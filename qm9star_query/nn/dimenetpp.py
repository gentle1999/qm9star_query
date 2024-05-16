try:
    import torch
    from dig.threedgraph.method.dimenetpp.dimenetpp import *
    from torch_geometric.data import Data
    from torch_scatter import scatter
    from torch.autograd import grad
except Exception as e:
    raise ImportError(
        """
This module requires additional dependencies.
Please install them following the instructions in README.md.
```bash
# cd <root dir of qm9star_query>
poetry install -E dl
```"""
    )


class DimeNetPPCM(torch.nn.Module):
    r"""
    The re-implementation for DimeNet++ from the `"Fast and Uncertainty-Aware Directional Message Passing for Non-Equilibrium Molecules" <https://arxiv.org/abs/2011.14115>`_ paper
    under the 3DGN gramework from `"Spherical Message Passing for 3D Molecular Graphs" <https://openreview.net/forum?id=givsRXsOt9r>`_ paper.

    Args:
        energy_and_force (bool, optional): If set to :obj:`True`, will predict energy and take the negative of the derivative of the energy with respect to the atomic positions as predicted forces. (default: :obj:`False`)
        cutoff (float, optional): Cutoff distance for interatomic interactions. (default: :obj:`5.0`)
        num_layers (int, optional): Number of building blocks. (default: :obj:`4`)
        hidden_channels (int, optional): Hidden embedding size. (default: :obj:`128`)
        out_channels (int, optional): Size of each output sample. (default: :obj:`1`)
        int_emb_size (int, optional): Embedding size used for interaction triplets. (default: :obj:`64`)
        basis_emb_size (int, optional): Embedding size used in the basis transformation. (default: :obj:`8`)
        out_emb_channels (int, optional): Embedding size used for atoms in the output block. (default: :obj:`256`)
        num_spherical (int, optional): Number of spherical harmonics. (default: :obj:`7`)
        num_radial (int, optional): Number of radial basis functions. (default: :obj:`6`)
        envelop_exponent (int, optional): Shape of the smooth cutoff. (default: :obj:`5`)
        num_before_skip (int, optional): Number of residual layers in the interaction blocks before the skip connection. (default: :obj:`1`)
        num_after_skip (int, optional): Number of residual layers in the interaction blocks before the skip connection. (default: :obj:`2`)
        num_output_layers (int, optional): Number of linear layers for the output blocks. (default: :obj:`3`)
        act: (function, optional): The activation funtion. (default: :obj:`swish`)
        output_init: (str, optional): The initialization fot the output. It could be :obj:`GlorotOrthogonal` and :obj:`zeros`. (default: :obj:`GlorotOrthogonal`)
    """

    def __init__(
        self,
        energy_and_force=False,
        cutoff=5.0,
        num_layers=4,
        hidden_channels=128,
        out_channels=1,
        int_emb_size=64,
        basis_emb_size=8,
        out_emb_channels=256,
        num_spherical=7,
        num_radial=6,
        envelope_exponent=5,
        num_before_skip=1,
        num_after_skip=2,
        num_output_layers=3,
        act=swish,
        output_init="GlorotOrthogonal",
        ret_res_dict=False,
    ):
        super(DimeNetPPCM, self).__init__()

        self.cutoff = cutoff
        self.energy_and_force = energy_and_force
        self.ret_res_dict = ret_res_dict
        self.init_ez = init(num_radial, hidden_channels, act)
        self.init_ec = init(num_radial, hidden_channels, act)
        self.init_em = init(num_radial, hidden_channels, act)
        self.init_v = update_v(
            hidden_channels,
            out_emb_channels,
            out_channels,
            num_output_layers,
            act,
            output_init,
        )
        self.init_u = update_u()
        self.emb = emb(num_spherical, num_radial, self.cutoff, envelope_exponent)

        self.update_vs = torch.nn.ModuleList(
            [
                update_v(
                    hidden_channels,
                    out_emb_channels,
                    out_channels,
                    num_output_layers,
                    act,
                    output_init,
                )
                for _ in range(num_layers)
            ]
        )

        self.update_es = torch.nn.ModuleList(
            [
                update_e(
                    hidden_channels,
                    int_emb_size,
                    basis_emb_size,
                    num_spherical,
                    num_radial,
                    num_before_skip,
                    num_after_skip,
                    act,
                )
                for _ in range(num_layers)
            ]
        )

        self.update_us = torch.nn.ModuleList([update_u() for _ in range(num_layers)])

        self.reset_parameters()

    def reset_parameters(self):
        self.init_ez.reset_parameters()
        self.init_ec.reset_parameters()
        self.init_em.reset_parameters()
        self.init_v.reset_parameters()
        self.emb.reset_parameters()
        for update_e in self.update_es:
            update_e.reset_parameters()
        for update_v in self.update_vs:
            update_v.reset_parameters()

    def forward(self, batch_data):
        try:
            z, pos, batch, chrg, mul = (
                batch_data["nxyz"][:, 0].clone().detach().to(torch.int64),
                batch_data["nxyz"][:, 1:],
                batch_data["batch"],
                batch_data["formal_charges"] + 8,
                batch_data["formal_num_radicals"],
            )
        except:
            z, pos, batch, chrg, mul = (
                batch_data["nxyz"][:, 0].clone().detach().to(torch.int64),
                batch_data["nxyz"][:, 1:],
                batch_data["mol_idx"],
                torch.zeros_like(batch_data["nxyz"][:, 0]).to(torch.int64) + 8,
                torch.zeros_like(batch_data["nxyz"][:, 0]).to(torch.int64),
            )

        if self.energy_and_force:
            pos.requires_grad_()
        edge_index = radius_graph(pos, r=self.cutoff, batch=batch)
        num_nodes = z.size(0)
        dist, angle, i, j, idx_kj, idx_ji = xyz_to_dat(
            pos, edge_index, num_nodes, use_torsion=False
        )

        emb = self.emb(dist, angle, idx_kj)

        # Initialize edge, node, graph features
        ez = self.init_ez(z, emb, i, j)
        ec = self.init_ec(chrg, emb, i, j)
        em = self.init_em(mul, emb, i, j)
        e = (ez[0] + ec[0] + em[0], ez[1] + ec[1] + em[1])
        v = self.init_v(e, i)
        u = self.init_u(
            torch.zeros_like(scatter(v, batch, dim=0)), v, batch
        )  # scatter(v, batch, dim=0)

        for update_e, update_v, update_u in zip(
            self.update_es, self.update_vs, self.update_us
        ):
            e = update_e(e, emb, idx_kj, idx_ji)
            v = update_v(e, i)
            u = update_u(u, v, batch)  # u += scatter(v, batch, dim=0)
        # results = {'energy':u}
        if self.ret_res_dict and self.energy_and_force:
            results = {"energy": u}
            energy_grad = grad(
                outputs=u,
                inputs=pos,
                grad_outputs=torch.ones_like(u),
                create_graph=True,
                retain_graph=True,
            )[0]
            results["energy_grad"] = energy_grad
            return results
        elif self.ret_res_dict and not self.energy_and_force:
            return {"energy": u}
        return u
