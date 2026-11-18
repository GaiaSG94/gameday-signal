import type { PuzzleResponse, SubmitRequest, SubmitResponse } from './puzzle';

export type { PuzzleResponse, SubmitRequest, SubmitResponse };

export type ErrorResponse = {
  status: 'error';
  message: string;
};
