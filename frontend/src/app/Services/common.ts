import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
@Injectable({
    providedIn: 'root'
})
export class CommonService {
    constructor(private http: HttpClient) { }

    private apiUrl = 'http://localhost:8000/api/';

    uploadDocuments(files: File[]): Observable<any> {
        const formData = new FormData();
        files.forEach((file) => {
            formData.append('files', file);
        });
        return this.http.post(this.apiUrl + 'documents/upload', formData);
    }

    sendMessage(payload: {
        question: string,
        organization_id: string
    }): Observable<any> {
        return this.http.post(`${this.apiUrl}chat`, payload);
    }
}