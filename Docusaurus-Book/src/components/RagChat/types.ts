export interface Message {
  type: 'user' | 'bot';
  text: string;
}

export interface Source {
  url: string;
  chunk: string;
}

export interface ChatState {
  messages: Message[];
  sources: Source[];
  isLoading: boolean;
  error: string | null;
}
