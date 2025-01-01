import { Component, OnInit } from '@angular/core';
import { PaymentService } from '../../services/payment.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})

export class DashboardComponent implements OnInit {
  constructor(private paymentService: PaymentService,) {
    console.log('Dashboard constructor called');
  }

  ngOnInit(): void {
    console.log("dashbaord entry")
  }
}