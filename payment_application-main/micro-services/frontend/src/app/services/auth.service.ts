// frontend/src/app/services/auth.service.ts
import { Injectable, PLATFORM_ID, Inject } from "@angular/core";
import { isPlatformBrowser } from '@angular/common';
import { tap } from 'rxjs/operators';

import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from '../../environments/environment';
import { LoginRequest, LoginResponse } from '../models/user.model';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = environment.authServiceUrl;

  constructor(private http: HttpClient,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {

  }
  private currentUserSubject = new BehaviorSubject<LoginResponse | null>(null);
  currentUser$ = this.currentUserSubject.asObservable()

  private getStorage(): Storage | null {
    if (isPlatformBrowser(this.platformId)) {
      return localStorage;
    }
    return null;
  }

  // get stored jwt token
  getToken(): string | null {
    const storage = this.getStorage();
    const token = storage ? storage.getItem("token") : null;
    // console.log('Retrieved token:', token);
    return token;
  }
  // check authentication stauts
  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  // This is the getter method that should be used instead of currentUserValue
  getCurrentUser(): LoginResponse | null {
    return this.currentUserSubject.value;
  }

  // login
  login(userData: LoginRequest): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.apiUrl}/login`, userData)
        .pipe(
            tap(response => {
                const storage = this.getStorage();
                // console.log(response)
                if (storage && response.access_token) {
                    storage.setItem('token', response.access_token);
                    // console.log('Retrieved tokens:', response.access_token);
                }
                else {
                    console.log('no Retrieved tokens:', response.access_token);
                }
            })
        );

}



  // login(userData: LoginRequest) {
  //   return this.http.post<LoginResponse>(`${this.apiUrl}/login`, userData)
  //     .pipe(map(response => {
  //       localStorage.setItem('token', JSON.stringify(response));
  //       this.currentUserSubject.next(response);
  //       return response;
  //     }));
  // }

  logout() {
    localStorage.removeItem('token');
    this.currentUserSubject.next(null);
  }

}