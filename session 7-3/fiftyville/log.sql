-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT description FROM crime_scene_reports
WHERE year = 2021 AND month = 7 AND day = 28 AND street = 'Humphrey Street';


SELECT name FROM people
JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate
WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10
  AND minute >= 15 AND minute <= 25 AND activity = 'exit';


SELECT name FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE atm_transactions.year = 2021 AND atm_transactions.month = 7 AND atm_transactions.day = 28
  AND atm_transactions.atm_location = 'Leggett Street' AND transaction_type = 'withdraw';


SELECT name FROM people
WHERE name IN (
  SELECT name FROM people
  JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate
  WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10
    AND minute >= 15 AND minute <= 25 AND activity = 'exit'
) AND id IN (
  SELECT person_id FROM bank_accounts
  JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
  WHERE atm_transactions.year = 2021 AND atm_transactions.month = 7 AND atm_transactions.day = 28
    AND atm_transactions.atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
);


SELECT transcript FROM interviews
WHERE year = 2021 AND month = 7 AND day = 28;


SELECT * FROM flights
JOIN airports ON origin_airport_id = airports.id
WHERE year = 2021 AND month = 7 AND day = 29 AND origin_city = 'Fiftyville'
ORDER BY hour, minute
LIMIT 1;


SELECT name FROM people
JOIN passports ON people.passport_number = passports.passport_number
JOIN passenger ON passports.id = passenger.passport_number
WHERE passenger.flight_id = 36;


SELECT name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.receiver
WHERE phone_calls.year = 2021 AND phone_calls.month = 7 AND phone_calls.day = 28
  AND phone_calls.duration < 60
  AND phone_calls.caller = (
    SELECT phone_number FROM people WHERE name = 'Taylor'
  );
