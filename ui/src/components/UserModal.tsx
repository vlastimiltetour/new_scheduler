import React from 'react';
import { User } from './UserTable';

interface FormData {
  name: string;
  email: string;
  role: string;
}

interface UserModalProps {
  isOpen: boolean;
  editingUser: User | null;
  formData: FormData;
  setFormData: React.Dispatch<React.SetStateAction<FormData>>;
  onSubmit: (e: React.FormEvent) => void;
  onClose: () => void;
}

export const UserModal: React.FC<UserModalProps> = ({
  isOpen,
  editingUser,
  formData,
  setFormData,
  onSubmit,
  onClose,
}) => {
  if (!isOpen && !editingUser) return null;

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div className="bg-white border border-gray-200 rounded-xl p-6 w-full max-w-md shadow-xl text-black">
        <h3 className="text-xl font-bold text-gray-900 mb-4">
          {editingUser ? '📝 Update User Profile' : '➕ Add New User Account'}
        </h3>

        <form onSubmit={onSubmit} className="flex flex-col gap-4">
          <div>
            <label className="block text-xs font-semibold uppercase text-gray-500 mb-1">
              Full Name
            </label>
            <input
              type="text"
              required
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="w-full border border-gray-300 p-2 rounded focus:outline-blue-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase text-gray-500 mb-1">
              Email Address
            </label>
            <input
              type="email"
              required
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              className="w-full border border-gray-300 p-2 rounded focus:outline-blue-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase text-gray-500 mb-1">
              System Context Role
            </label>
            <select
              value={formData.role}
              onChange={(e) => setFormData({ ...formData, role: e.target.value })}
              className="w-full border border-gray-300 p-2 rounded bg-white focus:outline-blue-500"
            >
              <option value="candidate">Candidate</option>
              <option value="interviewer">Interviewer</option>
            </select>
          </div>

          <div className="flex justify-end gap-2 mt-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border border-gray-300 text-gray-700 rounded hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded font-medium"
            >
              {editingUser ? 'Save Updates' : 'Confirm Save'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};