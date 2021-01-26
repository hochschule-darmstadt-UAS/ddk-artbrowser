import { Component, Input, Output, EventEmitter, AfterViewInit, ElementRef } from '@angular/core';
import { Entity } from 'src/app/shared/models/models';
import { Slide, makeDefaultSlide } from '../carousel.component';

/**
 * a slide of the slider.
 * if the image of an item cannot be loaded due to invalid url, the item is removed from the slider
 * and all following items move one position to the left to fill the gap.
 */
@Component({
  selector: 'app-slide',
  templateUrl: './slide.component.html',
  styleUrls: ['./slide.component.scss']
})
export class SlideComponent implements AfterViewInit {
  /** the slide that should be displayed */
  @Input() slide: Slide = makeDefaultSlide();

  /** emits hovered artwork on item hover event */
  @Output()
  itemHover: EventEmitter<Entity> = new EventEmitter<Entity>();

  /** trigger deletion of unused slides in slider component */
  @Output()
  deleteUnusedSlides: EventEmitter<void> = new EventEmitter<void>();

  constructor(private el: ElementRef) {}

  ngAfterViewInit() {
    if (window && 'IntersectionObserver' in window) {
      const obs = new IntersectionObserver(
        entries => {
          /** check whether any element of the slide is currently visible on screen */
          entries.forEach(({ isIntersecting }) => {
            if (isIntersecting) {
              /** enable image loading for this slide, the next slide and the previous slide if slide is visible */
              this.slide.loadContent = true;
              if (this.slide.nextSlide) {
                this.slide.nextSlide.loadContent = true;
              }
              if (this.slide.prevSlide) {
                this.slide.prevSlide.loadContent = true;
              }
              obs.unobserve(this.el.nativeElement);
            }
          });
        },
        { rootMargin: '100%' }
      );
      obs.observe(this.el.nativeElement);
    } else {
      this.slide.loadContent = true;
    }
  }

  /** if image of an item could not be loaded, shift succeeding items from this slide and following slides
   * one position to the left. if the last slide becomes empty during this process, delete the last slide.
   * @param item the item whose image could not be loaded
   */
  onLoadingError(item: Entity) {
    const itemIndex = this.slide.items.findIndex(i => {
      return i.id === item.id;
    });

    this.slide.items[itemIndex]['error'] = true;
  }
}
