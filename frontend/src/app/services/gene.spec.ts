import { TestBed } from '@angular/core/testing';

import { Gene } from './gene';

describe('Gene', () => {
  let service: Gene;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Gene);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
