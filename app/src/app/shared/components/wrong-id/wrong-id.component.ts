import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-wrong-id',
  templateUrl: './wrong-id.component.html',
  styleUrls: ['./wrong-id.component.scss']
})
export class WrongIdComponent implements OnInit {
  @Input() id: string;

  constructor() { }

  ngOnInit() {
  }

}
