
import { Routes } from '@angular/router';
import { DocumentUpload } from './features/document-upload/document-upload';

export const routes: Routes = [
  {
    path: 'upload',
    component: DocumentUpload
  },
  {
    path: '',
    redirectTo: 'upload',
    pathMatch: 'full'
  }
];
