import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { PaymentService } from '../../services/payment.service';
import { Payment } from '../../models/payment.model';

@Component({
  selector: 'app-transaction-history',
  templateUrl: './transaction-history.component.html', // Reference the HTML file
  styleUrls: ['./transaction-history.component.css'] // Reference the CSS file
})
export class TransactionHistoryComponent implements OnInit {
  payments: Payment[] = [];
  isLoading = false;
  errorMessage = '';

  constructor(private paymentService: PaymentService,
    private router: Router
  ) {}

  viewTransactionDetails(paymentId: string) {
    console.log("near transaction")
    console.log(paymentId,"tra hi id")
    this.router.navigate(['/transactions', paymentId]);
  }

  ngOnInit(): void {
    this.loadTransactions();
  }

  loadTransactions() {
    this.isLoading = true;
    this.errorMessage = '';

    this.paymentService.getPaymentHistory().subscribe({
      next: (payments: Payment[]) => {
        this.payments = payments;
      },
      error: (error: any) => {
        this.errorMessage = 'Failed to load transactions';
        console.error('Failed to load transactions:', error);
      },
      complete: () => {
        this.isLoading = false;
      }
    });
  }
}