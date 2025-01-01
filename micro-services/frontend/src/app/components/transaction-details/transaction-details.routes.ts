import { NgModule } from "@angular/core";
import { Routes,RouterModule } from "@angular/router";
import { TransactionDetailsComponent } from "./transaction-details.component";

// for empty path show the login component class
const routes:Routes = [
    {path:'',component:TransactionDetailsComponent}
];

// Configure child path and export
@NgModule({imports:[RouterModule.forChild(routes)],
            exports: [RouterModule]
})

export class TransactionDetailsRoutingModule {}