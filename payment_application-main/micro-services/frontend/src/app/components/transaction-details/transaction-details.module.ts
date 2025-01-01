import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TransactionDetailsComponent } from './transaction-details.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { TransactionDetailsRoutingModule } from './transaction-details.routes';


@NgModule({
  declarations: [TransactionDetailsComponent],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    TransactionDetailsRoutingModule
  ],
  exports: [TransactionDetailsComponent] // Export if you plan to use this component elsewhere
})
export class TransactionDetailsModule { }

