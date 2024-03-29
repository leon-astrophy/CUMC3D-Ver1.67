!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! This subroutine finds the speed of sound !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
SUBROUTINE EOSSOUNDSPEED(p_in, rho_in, eps_in, cs_out)
!$acc routine seq
USE DEFINITION
IMPLICIT NONE

! Input density !
REAL*8, INTENT (IN) :: p_in, rho_in, eps_in

! Output value !
REAL*8, INTENT (OUT) :: cs_out

! Local variables !
REAL*8 :: dpdden, dpdint

! We do the DM case first !
dpdden = eps_in * (ggas - 1.0D0)
dpdint = rho_in * (ggas - 1.0D0)
cs_out = DSQRT(dpdden+dpdint*p_in/(rho_in*rho_in))

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

contains

	REAL*8 function dpdx(x)
	!$acc routine seq
	implicit none
	REAL*8 :: x
	dpdx = 8.0D0*x**4/DSQRT(x**2 + 1.0D0)
	end function

END SUBROUTINE