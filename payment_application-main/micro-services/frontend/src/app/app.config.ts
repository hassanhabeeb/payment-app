// app.config.ts
import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import { provideClientHydration } from '@angular/platform-browser';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideHttpClient,  withInterceptorsFromDi , withFetch} from '@angular/common/http';
import { AuthInterceptor } from './interceptors/auth.interceptor';
import { HTTP_INTERCEPTORS } from '@angular/common/http';

export const appConfig: ApplicationConfig = {
    providers: [
        provideZoneChangeDetection({ eventCoalescing: true }),
        provideRouter(routes),
        provideClientHydration(),
        provideAnimationsAsync(),
        provideHttpClient(withInterceptorsFromDi(), withFetch()),  
{
  provide:HTTP_INTERCEPTORS,
  useClass:AuthInterceptor,
  multi:true
}
    ]
};