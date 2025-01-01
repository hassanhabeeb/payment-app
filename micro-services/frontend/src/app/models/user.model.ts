// frontend/src/app/models/user.model.ts
export interface LoginRequest {
    email: string;
    password: string
}

export interface User {
    id: string;
    email: string;
}




export interface LoginResponse {
    access_token: string;
    token_type: string;
    user?: User;
}