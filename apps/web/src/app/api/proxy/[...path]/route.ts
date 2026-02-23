import { NextRequest } from "next/server";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export async function GET(req: NextRequest, { params }: { params: { path: string[] } }) {
  const target = `${API_BASE}/${params.path.join("/")}${req.nextUrl.search}`;
  const res = await fetch(target, { cache: "no-store" });
  return new Response(await res.text(), {
    status: res.status,
    headers: { "content-type": res.headers.get("content-type") || "application/json" },
  });
}
