// frontend/src/app/interceptors/auth.interceptor.ts
import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpErrorResponse
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { isPlatformBrowser } from '@angular/common';

import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(
    private authService: AuthService,
    @Inject(PLATFORM_ID) private platformId: Object
  ) { }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {

    // Skip for login requests
    if (request.url.includes('/login')) {
      return next.handle(request);
    }
    // Only attach token in browser environment
    if (isPlatformBrowser(this.platformId)) {
      const token = this.authService.getToken();

      if (token) {
        request = request.clone({
          setHeaders: {
            'Authorization': `Bearer ${token}`  // Fixed template literal
          }
        });
        console.log('Request with auth headers:', request.headers.get('Authorization')); // Debug log
      }
    }

    return next.handle(request);
  }
}