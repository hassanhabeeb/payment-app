import { NgModule } from "@angular/core";
import { Routes,RouterModule } from "@angular/router";
import { DashboardComponent} from "./dashboard.component";

// for empty path show the login component class
const routes:Routes = [
    {path:'',component:DashboardComponent}
];

// Configure child path and export
@NgModule({imports:[RouterModule.forChild(routes)],
            exports: [RouterModule]
})

export class DashboardRoutingModule {}