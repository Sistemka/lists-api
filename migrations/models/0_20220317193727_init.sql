-- upgrade --
CREATE TABLE IF NOT EXISTS "lists" (
    "object_id" SERIAL NOT NULL PRIMARY KEY,
    "id" UUID NOT NULL UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL,
    "updated_at" TIMESTAMPTZ NOT NULL,
    "header" VARCHAR(255) NOT NULL,
    "text" TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_lists_id_9a36f4" ON "lists" USING HASH ("id");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
