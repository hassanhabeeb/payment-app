// frontend/src/app/guards/auth.guard.ts
import { Injectable, PLATFORM_ID, Inject } from "@angular/core";
import { isPlatformBrowser } from '@angular/common';
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from "@angular/router";
import { AuthService } from '../services/auth.service';

@Injectable(
  { providedIn: 'root' }
)

export class AuthGuard implements CanActivate {
  constructor(
    private authService: AuthService,
    private router: Router,
    @Inject(PLATFORM_ID) private platformId: Object
  ) { }

  canActivate(next: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    if (!isPlatformBrowser(this.platformId)) {
      console.log("activate0")
      return true; // Allow access during SSR
    }
    console.log("activate00",this.authService.isAuthenticated())
    if (this.authService.isAuthenticated()) {
      console.log("activate000",this.authService.isAuthenticated())
      return true
    }
    this.router.navigate(['/login'])
    return false
  }
}