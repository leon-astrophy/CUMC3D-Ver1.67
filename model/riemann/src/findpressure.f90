!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! This subroutine update the pressure profile and their deriative    !
! once the density profile is being updated through rungekutta time  !
! evolution. It is being used in every time step, do not confused it !
! with subroutine GETRHOEOSRTOP                                      !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
SUBROUTINE FINDPRESSURE
USE DEFINITION
IMPLICIT NONE

! Integer !
INTEGER :: i, j, k, l

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

! The following steps are more or less similar , so no repeat 
!$OMP PARALLEL DO COLLAPSE(3) SCHEDULE(STATIC)
!$ACC PARALLEL LOOP GANG WORKER VECTOR COLLAPSE(3) DEFAULT(PRESENT)
DO l = -2, nz + 3
	DO k = -2, ny + 3
		DO j = -2, nx + 3
      prim(itau,j,k,l) = prim(irho,j,k,l) * epsilon(j,k,l) * (ggas - 1.0D0) 
      dpdrho (j,k,l) = epsilon(j,k,l) * (ggas - 1.0D0)
      dpdeps (j,k,l) = prim(irho,j,k,l) * (ggas - 1.0D0)
      cs(j,k,l) = DSQRT(dpdrho(j,k,l)+dpdeps(j,k,l)*prim(itau,j,k,l)/(prim(irho,j,k,l)*prim(irho,j,k,l)))
    END DO
  END DO
END DO
!$ACC END PARALLEL
!$OMP END PARALLEL DO

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

contains

  REAL*8 function large_pressure(x)
  !$acc routine SEQ
  implicit none
  REAL*8 :: x
  large_pressure = x*DSQRT(x**2 + 1.0D0)*(2.0D0*x**2 - 3.0D0) + 3.0D0*log(x + DSQRT(x**2 + 1.0D0))
  end function

  REAL*8 function small_pressure(x)
  !$acc routine SEQ
  implicit none
  REAL*8 :: x
  small_pressure = 1.6D0*x**5 - (4.0D0/7.0D0)*x**7 + (1.0D0/3.0D0)*x**9 - (5.0D0/2.2D1)*x**11 & 
      + (3.5D1/2.08D2)*x**13 - (2.1D1/1.6D2)*x**15 + (2.31D2/2.176D3)*x**17
  end function

END SUBROUTINE

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! This subroutine finds the specific internal energy !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
SUBROUTINE EOSPRESSURE_NM (rho_in, eps_in, p_out)
!$acc routine SEQ
USE DEFINITION
IMPLICIT NONE

! Input density !
REAL*8, INTENT (IN) :: rho_in, eps_in

! Output value !
REAL*8, INTENT (OUT) :: p_out

! For DM/NM, choose by type !
p_out = rho_in * eps_in ** (ggas - 1.0D0)

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

contains

	REAL*8 function fermi_large_pressure(x)
  !$acc routine SEQ
	implicit none
	REAL*8 :: x
	fermi_large_pressure = x*DSQRT(x**2 + 1.0D0)*(2.0D0*x**2 - 3.0D0) + 3.0D0*log(x + DSQRT(x**2 + 1.0D0))
	end function

	REAL*8 function fermi_small_pressure(x)
  !$acc routine SEQ
	implicit none
	REAL*8 :: x
	fermi_small_pressure = 1.6D0*x**5 - (4.0D0/7.0D0)*x**7 + (1.0D0/3.0D0)*x**9 - (5.0D0/2.2D1)*x**11 & 
			+ (3.5D1/2.08D2)*x**13 - (2.1D1/1.6D2)*x**15 + (2.31D2/2.176D3)*x**17
	end function

END SUBROUTINE