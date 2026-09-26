export interface User {
  id: string | number;
  name: string;
  email: string;
  role: string;
}

export interface UserFormData {
  name: string;
  email: string;
  role: string;
}