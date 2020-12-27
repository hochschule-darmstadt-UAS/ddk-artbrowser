import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { TypeComponent } from './type.component';
import { SharedModule } from '../../shared/shared.module';

const motifRoutes: Routes = [
  {
    path: '',
    component: TypeComponent
  }
];

@NgModule({
  declarations: [TypeComponent],
  imports: [CommonModule, SharedModule, RouterModule.forChild(motifRoutes)],
  exports: [TypeComponent]
})
export class TypeRoutingModule {}
