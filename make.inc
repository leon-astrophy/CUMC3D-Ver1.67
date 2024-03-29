######################################################
#
# make.inc file incluing compilation flags for CUMC3D
#
######################################################

# Want to fix singularies pole? #
FIXPOLE = -DFIXPOLE 

# Want to debug? #
#DEBUG = -DDEBUG

# Want to get divergence of B? #
DIVB = -DDIVB

# Want to look for compilation message? #
#COMPILE = -Minfo=accel

# Choose between CPU or GPU threading #
MULTICORE = -DGPU -acc
#MULTICORE = -mp

# Define F90 compiler #
F90=/home/leon/HDF5/bin/h5fc

# Define F90 flags #
F90FLAGS= -llapack -lblas -cpp -fastsse -Mipa=fast -O4 -Mvect=simd -Mvect=levels:5 -Msmartalloc -Mstack_arrays -Mprefetch $(MULTICORE) $(COMPILE) $(DEBUG) $(DIVB) $(FIXPOLE)
LDFLAGS= -llapack -lblas -cpp -fastsse -Mipa=fast -O4 -Mvect=simd -Mvect=levels:5 -Msmartalloc -Mstack_arrays -Mprefetch $(MULTICORE) $(COMPILE) $(DEBUG) $(DIVB) $(FIXPOLE)
