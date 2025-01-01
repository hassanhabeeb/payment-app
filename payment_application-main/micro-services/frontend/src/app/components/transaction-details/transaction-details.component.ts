// transaction-details.component.ts
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { PaymentService } from '../../services/payment.service';
import { Payment } from '../../models/payment.model';

@Component({
  selector: 'app-transaction-details',
  templateUrl: './transaction-details.component.html',
  styleUrls: ['./transaction-details.component.css']
})
export class TransactionDetailsComponent implements OnInit {
  payment?: Payment;
  isLoading = false;
  errorMessage = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private paymentService: PaymentService
  ) {}

  ngOnInit(): void {
    console.log("details initialized")
    this.route.params.subscribe(params => {
      const id = params['id'];
      if (id) {
        console.log(id,"tra hi id")
        this.loadTransactionDetails(id);
      }
    });
  }

  loadTransactionDetails(id: string) {
    this.isLoading = true;
    this.paymentService.getPayment(id).subscribe({
      next: (payment) => {
        this.payment = payment;
        this.isLoading = false;
      },
      error: (error) => {
        this.errorMessage = 'Failed to load transaction details';
        this.isLoading = false;
      }
    });
  }

  goBack() {
    this.router.navigate(['/dashboard']);
  }
}