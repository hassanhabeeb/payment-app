import { Component } from '@angular/core';
import { PaymentService } from '../../services/payment.service';
// import { TransactionHistoryComponent } from '../transaction-history/transaction-history.component';

@Component({
  selector: 'app-payment-form',
  templateUrl: './payment-form.component.html', // Reference the HTML file
  styleUrls: ['./payment-form.component.css'] // Reference the CSS file
})
export class PaymentFormComponent {
  payment = {
    amount: 0,
    currency: 'USD',
    description: '',
    payment_method: 'card'
  };
  isLoading = false;
  errorMessage = '';
  successMessage = '';

  constructor(private paymentService: PaymentService
  ) {}

  onSubmit() {
    if (this.payment.amount <= 0) {
      this.errorMessage = 'Amount must be greater than 0';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';
    this.successMessage = '';

    this.paymentService.createPayment(this.payment)
      .subscribe({
        next: (response) => {
          this.successMessage = 'Payment successful';
          // this.history.loadTransactions()
          this.resetForm();
        },
        error: (error) => {
          this.errorMessage = error.error.detail || 'Payment failed';
        },
        complete: () => {
          this.isLoading = false;
        }
      });
  }

  private resetForm() {
    this.payment = {
      amount: 0,
      currency: 'USD',
      description: '',
      payment_method: 'card'
    };
  }
}