import api from "./api";

export interface Workspace {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  owner_id: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateWorkspacePayload {
  name: string;
  slug: string;
  description?: string | null;
}

export const workspaceApi = {
  async list(): Promise<Workspace[]> {
    const response = await api.get<Workspace[]>("/workspaces");

    return response.data;
  },

  async get(workspaceId: string): Promise<Workspace> {
    const response = await api.get<Workspace>(
      `/workspaces/${workspaceId}`,
    );

    return response.data;
  },

  async create(
    payload: CreateWorkspacePayload,
  ): Promise<Workspace> {
    const response = await api.post<Workspace>(
      "/workspaces",
      payload,
    );

    return response.data;
  },

  async remove(workspaceId: string): Promise<void> {
    await api.delete(`/workspaces/${workspaceId}`);
  },
};