import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './guards/auth.guard';

export const routes: Routes = [
  { path: 'login', loadChildren: () => import('./components/login/login.module').then(m => m.LoginModule) },
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  {
    path: 'dashboard',
    loadChildren: () => import('./components/dashboard/dashboard.module').then(m => m.DashboardModule),
    canActivate: [AuthGuard]
  },
  {
    path: 'transactions/:id',
    loadChildren: () => import('./components/transaction-details/transaction-details.module').then(m => m.TransactionDetailsModule),
    canActivate: [AuthGuard]
  }
  
];







@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
  })
  export class AppRoutingModule {
    
  }


