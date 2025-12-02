from fenics import *
import ufl_legacy as ufl
from dolfin import *

#     |-------------------------------------------------------------------------|
#     |   This code aims to apply a simple exemple of a heat transfer exercise  |
#     |               a plane wall to validate the FeNiCs prompt                |
#     |-------------------------------------------------------------------------|

# First, it is necessary to define the goemtry and the mesh (Box mesh)

polynomial_degree = 1

# Defines the lenght of the edges (in his case: parameters fo the exeercise 2.12 
# of the 7th ed. Heat and Mass Transfer Incropera


L = 0.1
W = 1.0
H = 1.0

# Defines the prescribed temperatues conditions 

T_hot = 600.0
T_cold = 400.0

# We are considering a total isotropic material, thus, the sencond order tensor 
# of the condutivity is gonna be k*I, where I is the identity tensor 

k = 100.0

I = Identity(3)

k_tensor = k*I

mesh = BoxMesh(Point(0.0, 0.0, 0.0), Point(L, H, W), 5, 10, 10)

# Defines the function Space

V = FunctionSpace(mesh, 'P', polynomial_degree)

# Boundary conditions 

tol = 1e-10

# Defines where each volume or facet is localized

left_facet = CompiledSubDomain("near(x[0], 0)")
right_facet = CompiledSubDomain("near(x[0], L)", L=L)
volume_1 = CompiledSubDomain("x[1]<= h + tol", h=H, tol=tol)

# Defines the number of each part defined previously

boundary_markers = MeshFunction("size_t", mesh, mesh.topology().dim()-1)
boundary_markers.set_all(0)
left_facet.mark(boundary_markers, 1)
right_facet.mark(boundary_markers, 2)

volume_markers = MeshFunction("size_t", mesh, mesh.topology().dim())
volume_markers.set_all(0)
volume_1.mark(volume_markers, 3)

# Defines the Dirichlet boundary consitions

bc_hot = DirichletBC(V, Constant(T_hot), left_facet)
bc_cold = DirichletBC(V, Constant(T_cold), right_facet)

# Put in a list

bc = [bc_hot, bc_cold]

# ************************************************************
#                         variational Form                   *
# ************************************************************

T = TrialFunction(V)

delta_T = TestFunction(V)

# To test, first, we can define the energy generation as constant zero

q_v = Constant(0.0)

# Recording coersivity, as shown by Larx Milgran, the bilinear and linear parts are:

# We have only one volume, thus:

dx = Measure("dx", domain=mesh, subdomain_data=volume_markers)

# bilinear part

a = dot(k_tensor*grad(T), grad(delta_T)) * dx

# linear part (if had heat flux prescribed, it would be necessary to apply more one part: 
# (heat_flux * delta_T * ds(number of the face)

l = q_v * delta_T * dx

# Solve 

T_solve = Function(V, name = "Temperature")

solve(a == l, T_solve, bc)

# ************************************************************
#                 Projection of the heat_flux                *
# ************************************************************

W = VectorFunctionSpace(mesh, 'P', polynomial_degree)

# We know that: heat_flux = -K * grad(T)

flux_equation = -1.0 * k_tensor * grad(T_solve)

flux_solve = project(flux_equation, W, solver_type="cg")
flux_solve.rename("Heat Flux", "Heat Flux Vector")

# ************************************************************
#                         Save in a file                     *
# ************************************************************

xdmf_file = XDMFFile("Results_heat_transfer.xdmf")

xdmf_file.write(T_solve, 0.0)
xdmf_file.write(flux_solve, 0.0)

xdmf_file.close()







