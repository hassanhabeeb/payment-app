import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { first } from 'rxjs/operators';
import { FormBuilder, FormGroup, Validators } from "@angular/forms";

import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  loginForm: FormGroup;
  
  email: string = '';
  password: string = '';
  loading = false;
  error = '';
  returnUrl: string = '/dashboard';

  constructor(
    private authService: AuthService,
    private fb: FormBuilder,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.loginForm = this.fb.group({'email': ['', Validators.required],
      'password': ['', Validators.required]})

    // redirect to dashboard if already logged in
    // if (this.authService.getCurrentUser()) {
    //   this.router.navigate(['/dashboard']);
    // }
  }

  ngOnInit() {
    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/dashboard';
  }

  onSubmit() {
    this.router.navigate(["/dashboard"]);
    if (! this.loginForm.valid) {
      this.error = "Please fill in all required fields";
      return;
    }

    this.loading = true;
    this.error = '';

    this.authService.login(this.loginForm.value).subscribe({
      next: (response) => {
        console.log("Login response received:", response);
        this.router.navigate(["/dashboard"]);
      },
      error: (error) => {
        console.log("Error details:", {
          status: error.status,
          message: error.message,
          error: error
        });
        
        // More specific error handling
        if (error.status === 401) {
          this.error = "Invalid username or password";
        } else if (error.status === 404) {
          this.error = "Server not found";
        } else {
          this.error = `Login failed: ${error.message || 'Unknown error'}`;
        }
        this.loading = false;
      }
    });
  }
}