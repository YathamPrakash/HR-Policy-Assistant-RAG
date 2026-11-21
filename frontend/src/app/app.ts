import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CommonService } from '../app/Services/common';
import { finalize, pipe } from 'rxjs';
import { ChangeDetectorRef } from '@angular/core';
interface DocumentItem {
  id: number;
  name: string;
  size: string;
  status: 'Completed' | 'Processing' | 'Failed';
}

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  time: string;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
  ],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  constructor(private commonservice: CommonService, private cdr: ChangeDetectorRef) { }
  activePage: 'totalDocuments' | 'chat' = 'totalDocuments';
  question = '';
  selectedFiles: File[] = [];
  totalDocuments: DocumentItem[] = [];

  messages: ChatMessage[] = [
    {
      role: 'assistant',
      content: 'Hello! I am KnowSphere AI. Ask me anything about your uploaded documents.',
      time: 'Just now'
    }
  ];

  setPage(page: 'totalDocuments' | 'chat'): void {
    this.activePage = page;
  }

  removeSelectedFile(index: number): void {
    this.selectedFiles.splice(index, 1);
  }

  formatFileSize(size: number): string {
    if (size < 1024 * 1024) {
      return `${(size / 1024).toFixed(2)} KB`;
    }
    return `${(size / (1024 * 1024)).toFixed(2)} MB`;
  }


  get completedDocuments(): number {
    return this.totalDocuments.filter(
      document => document.status === 'Completed'
    ).length;
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    console.log(typeof (input))
    console.log(input?.files?.[0])

    if (!input.files?.length) return;

    const pdfFiles = Array.from(input.files).filter(
      file => {
        console.log(file, "each file");
        return file.type === 'application/pdf';
      }
    );
    console.log(pdfFiles, "pdf files");
    this.selectedFiles = [...this.selectedFiles, ...pdfFiles];
    console.log(this.selectedFiles, "selected files after update");
    input.value = '';
  }

  uploadFiles(): void {
    if (!this.selectedFiles.length) return;

    this.commonservice.uploadDocuments(this.selectedFiles).pipe(
      finalize(() => {
        console.log('Upload finalized');
      })
    ).subscribe({
      next: (response) => {
        const newDocuments: DocumentItem[] =
          response.uploaded_files.map((file: any, index: number) => ({
            id: Date.now() + index,
            name: file.filename,
            size: file.size,
            status: 'Completed'
          }));
        this.totalDocuments = [...newDocuments, ...this.totalDocuments];
        this.selectedFiles = [];
        this.cdr.markForCheck();
      },
      error: (error) => {
        console.error('Upload failed:', error);
        this.cdr.markForCheck();
      }
    });
  }

  currentTime = new Date().toLocaleTimeString('en-IN', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true
  });


  sendMessage(): void {
    const text = this.question.trim();

    if (!text) return;

    // Add user message
    this.messages = [
      ...this.messages,
      {
        role: 'user',
        content: text,
        time: this.currentTime
      }
    ];

    const payload = {
      question: text,
      organization_id: 'org_001'
    };

    this.question = '';

    this.commonservice.sendMessage(payload).subscribe({
      next: (response) => {
        console.log('Chat response: IN APP.TS', response);

        this.messages = [
          ...this.messages,
          {
            role: 'assistant',
            content: response.answer,
            time: this.currentTime
          }
        ];

        // Notify Angular to update the UI
        this.cdr.markForCheck();
      },

      error: (error) => {
        console.error('Chat failed:', error);
        this.cdr.markForCheck();
      }
    });
  }


}
