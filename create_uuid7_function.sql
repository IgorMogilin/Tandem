-- uuid_v7_function.sql
-- Расширение для генерации случайных байт
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Функция генерации UUID v7
CREATE OR REPLACE FUNCTION uuid_generate_v7()
RETURNS UUID
AS $$
DECLARE
  -- Текущее время в миллисекундах (48 бит)
  time_ms bigint := (extract(epoch from clock_timestamp()) * 1000)::bigint;
  -- Случайные байты (74 бита)
  random_bytes bytea := gen_random_bytes(10);
  -- Результирующий UUID как 16 байт
  result_bytes bytea;
BEGIN
  -- Конвертируем время в 8 байт и берем последние 6 (48 бит)
  result_bytes := decode(lpad(to_hex(time_ms), 16, '0'), 'hex');
  result_bytes := substring(result_bytes from 3);

  -- Добавляем случайные байты
  result_bytes := result_bytes || random_bytes;

  -- Устанавливаем версию 7 (биты 48-51 = 0111)
  result_bytes := set_byte(
    result_bytes,
    6,
    (b'0111'::bit(4)::int << 4) | (get_byte(result_bytes, 6) & 15)
  );

  -- Устанавливаем вариант RFC 4122 (биты 64-65 = 10)
  result_bytes := set_byte(
    result_bytes,
    8,
    (b'10'::bit(2)::int << 6) | (get_byte(result_bytes, 8) & 63)
  );

  -- Возвращаем как UUID
  RETURN encode(result_bytes, 'hex')::uuid;
END;
$$
LANGUAGE plpgsql
VOLATILE;
