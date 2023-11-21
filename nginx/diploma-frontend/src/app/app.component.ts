import { Component, HostListener, OnInit } from '@angular/core';
import { WebcamImage } from 'ngx-webcam';
import { HttpClient } from '@angular/common/http';
import { Subject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { v4 as uuidv4 } from 'uuid';
import { LogItem, Session } from './datatypes';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  webcamImage!: WebcamImage
  capturedImage!: String
  currentSessionId!: String
  isSessionActive: boolean = false
  showBrowseSessionModal = false
  showSessionDetailsModal = false
  loadedSessions!: Session[]
  browsedSessionDetails!: LogItem[]
  currentSession!: LogItem[]
  latestLog!: LogItem
  time = new Date().toLocaleTimeString()

  private trigger: Subject<any> = new Subject()
  private nextWebcam: Subject<any> = new Subject()

  constructor(private http: HttpClient) {
  }

  ngOnInit() {
    if (localStorage.getItem('isSessionActive').toString() === 'true') {
      this.currentSessionId = localStorage.getItem('sessionID')
      this.isSessionActive = true
    }

    setInterval(() => {
      this.time = new Date().toLocaleTimeString()
      if (this.isSessionActive) {
        this.getSnapshot()
        this.http.get(
          "https://api.19273.pl/api/sessions/" + this.currentSessionId + "/get-logs/")
          .subscribe((data) => this.currentSession = JSON.parse(JSON.stringify(data)))
      }
    }, 750)
  }

  sendFrameForDetection(webcamImage: WebcamImage): void {
    this.webcamImage = webcamImage
    this.capturedImage = webcamImage!.imageAsDataUrl

    this.http.post(
      'https://api.19273.pl/api/send-image-for-detection/',
      {
        image: this.capturedImage,
        session: { session_id: this.currentSessionId }
      })
      .pipe(map(response => response as any))
      .subscribe(response => console.log(response))
  }

  newSession() {

    // Closes current session
    if (this.currentSessionId) {
      this.http.post(
        "https://api.19273.pl/api/sessions/" + this.currentSessionId + "/close-session/", null)
        .pipe(map(response => response as any)).subscribe(response => console.log(response))
      this.currentSessionId = null
    }

    this.currentSessionId = uuidv4();
    this.isSessionActive = true
    localStorage.setItem('sessionID', this.currentSessionId.toString());
    localStorage.setItem('isSessionActive', 'true');
  }

  finishSession() {
    this.isSessionActive = false
    localStorage.setItem('sessionID', '');
    localStorage.setItem('isSessionActive', 'false');

    this.http.post(
      "https://api.19273.pl/api/sessions/" + this.currentSessionId + "/close-session/", null)
      .pipe(map(response => response as any)).subscribe(response => {
        console.log(response)
      })

    this.currentSessionId = null
    this.currentSession = null
  }

  getSnapshot(): void {
    this.trigger.next(void 0)
  }

  get invokeObservable(): Observable<any> {
    return this.trigger.asObservable()
  }

  get nextWebcamObservable(): Observable<any> {
    return this.nextWebcam.asObservable()
  }

  get videoOptions(): MediaTrackConstraints {
    const result: MediaTrackConstraints = {
      width: { min: 360, ideal: 1920 },
      height: { min: 200, ideal: 1080 }
    }

    return result;
  }

  openBrowseSessionModal() {
    this.http.get("https://api.19273.pl/api/sessions/")
      .subscribe((data) => this.loadedSessions = JSON.parse(JSON.stringify(data)))
    this.showBrowseSessionModal = true;
  }

  closeBrowseSessionModal() {
    this.showBrowseSessionModal = false;
  }

  openSessionDetailsModal(id: String) {
    this.http.get(
      "https://api.19273.pl/api/sessions/" + id + "/get-logs/")
      .subscribe((data) => this.browsedSessionDetails = JSON.parse(JSON.stringify(data)))
    this.showSessionDetailsModal = true
  }

  closeSessionDetailsModal() {
    this.showSessionDetailsModal = false
  }

  openImage(url: string) {
    window.open(url, "_blank")
  }

}
