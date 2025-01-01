// payment.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Payment } from '../models/payment.model';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class PaymentService {
  private apiUrl = environment.paymentServiceUrl;

  constructor(private http: HttpClient,
    private authService: AuthService
  ) { }

  private getHeaders(): HttpHeaders {
    const token = this.authService.getToken();
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`  
    });
  }

  createPayment(payment: any): Observable<any> {
    console.log(payment,"payments")
    return this.http.post(`${this.apiUrl}/payments`, payment, { headers: this.getHeaders() });
  }

  getPayment(id: string): Observable<any> {
    return this.http.get(`${environment.paymentServiceUrl}/payments/${id}`, { headers: this.getHeaders() });
  }

  getPaymentHistory(): Observable<Payment[]> {
    return this.http.get<Payment[]>(`${this.apiUrl}/history`, { headers: this.getHeaders() }); 
  }
}