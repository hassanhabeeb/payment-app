export interface Payment {
  id: string;
  amount: number;
  currency: string;
  description: string;
  payment_method: string;
  status: string;
  created_at: Date;
  user_email: string;
}