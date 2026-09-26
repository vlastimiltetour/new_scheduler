import React from 'react';

export interface User {
  id: string | number;
  name: string;
  email: string;
  role: string;
}

interface UserTableProps {
  users: User[];
  loading: boolean;
  onEdit: (user: User) => void;
  onDelete: (id: string | number, name: string) => void;
  onDetail: (id: string | number) => void;
}

export const UserTable: React.FC<UserTableProps> = ({
  users,
  loading,
  onEdit,
  onDelete,
  onDetail,
}) => {
  return (
    <div className="w-full overflow-x-auto border border-gray-200 rounded-lg shadow-sm">
      <table className="w-full text-left border-collapse">
        <thead>
          <tr className="bg-gray-50 border-b border-gray-200 text-gray-700 font-medium">
            <th className="p-4">Name</th>
            <th className="p-4">Email</th>
            <th className="p-4">Role</th>
            <th className="p-4 text-center w-24">Update</th>
            <th className="p-4 text-center w-24">Delete</th>
            <th className="p-4 text-center w-24">Detail</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200 text-gray-600">
          {loading ? (
            <tr>
              <td colSpan={6} className="p-8 text-center text-gray-400 italic">
                Loading from FastAPI...
              </td>
            </tr>
          ) : users.length === 0 ? (
            <tr>
              <td colSpan={6} className="p-8 text-center text-gray-400 italic">
                No records present.
              </td>
            </tr>
          ) : (
            users.map((user) => (
              <tr key={user.id} className="hover:bg-gray-50 transition-colors">
                <td className="p-4 font-bold text-gray-900">{user.name}</td>
                <td className="p-4">{user.email}</td>
                <td className="p-4 uppercase text-xs tracking-wider">{user.role}</td>
                
                <td className="p-4 text-center">
                  <button onClick={() => onEdit(user)} className="hover:scale-125 transition-transform">
                    📝
                  </button>
                </td>
                <td className="p-4 text-center">
                  <button onClick={() => onDelete(user.id, user.name)} className="hover:scale-125 transition-transform">
                    ❌
                  </button>
                </td>
                <td className="p-4 text-center">
                  <button onClick={() => onDetail(user.id)} className="hover:scale-125 transition-transform">
                    👁️
                  </button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
};