-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description FROM crime_scene_reports WHERE month = 7 AND day = 28 AND street = 'Humphrey Street';

-- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today
--with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.

SELECT transcript FROM interviews WHERE year = 2023 AND month = 7 AND day = 28;

--“Ah,” said he, “I forgot that I had not seen you for some weeks. It is a little souvenir from the King of Bohemia in return for my assistance in the case of the Irene Adler papers.”
--“I suppose,” said Holmes, “that when Mr. Windibank came back from France he was very annoyed at your having gone to the ball.”
--“You had my note?” he asked with a deep harsh voice and a strongly marked German accent. “I told you that I would call.” He looked from one to the other of us, as if uncertain which to address.
--Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.
--I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.
--As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.
--Our neighboring courthouse has a very annoying rooster that crows loudly at 6am every day. My sons Robert and Patrick took the rooster to a city far, far away, so it may never bother us again. My sons have successfully arrived in Paris.

SELECT license_plate FROM bakery_security_logs WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND 15<= minute <= 25;

--R3G7486
--13FNH73
--5P2BI95
--94KL13X
--6P58WS2
--4328GD8
--G412CB7
--L93JTIZ
--322W7JE
--0NTHK55
--1106N58
--NRYN856
--WD5M8I6
--V47T75I

SELECT people.name from people
JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate
WHERE bakery_security_logs.day = 28 AND bakery_security_logs.month = 7
AND bakery_security_logs.year = 2023 AND bakery_security_logs.hour = 10
AND bakery_security_logs.minute BETWEEN 15 AND 25;

--Vanessa
--Bruce
--Barry
--Luca
--Sofia
--Iman
--Diana
--Kelsey

SELECT people.name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE phone_calls.year = 2023 AND phone_calls.month = 7 AND phone_calls.day = 28
AND phone_calls.duration <= 60;

--Caller, duration <=60
--Kenny
--Sofia
--Benista
--Taylor
--Diana
--Kelsey
--Kathryn
--Bruce
--Carina


SELECT name
FROM people
WHERE id IN (
    SELECT person_id
    FROM bank_accounts
    WHERE account_number IN (
        SELECT account_number
        FROM atm_transactions
        WHERE year = 2023
        AND month = 7
        AND day = 28
        AND atm_location = 'Leggett Street'
        AND transaction_type = 'withdraw'
    )
);

--Bank transactions
--Kenny
--Iman
--Benista
--Taylor
--Brooke
--Luca
--Diana
--Bruce !!!


------------------------------------------------------------------------------------

SELECT name FROM people
WHERE passport_number IN
(
    SELECT passport_number FROM passengers
    WHERE flight_id IN
    (
        SELECT id FROM flights
        WHERE year = 2023 AND month = 7 AND day = 29 AND origin_airport_id = 8
    )
);

--Indeed, on the flight was Bruce


SELECT hour FROM flights WHERE year = 2023 AND month = 7 AND day = 29 AND origin_airport_id = 8 AND id IN
(
    SELECT flight_id FROM passengers
    WHERE passport_number IN
    (
        SELECT passport_number FROM people
        WHERE name = 'Bruce'
    )
);

--8 am

SELECT city FROM airports WHERE id IN
(
    SELECT destination_airport_id FROM flights WHERE year = 2023 AND month = 7 AND day = 29 AND origin_airport_id = 8 AND id IN
    (
        SELECT flight_id FROM passengers
        WHERE passport_number IN
        (
            SELECT passport_number FROM people
            WHERE name = 'Bruce'
        )
    )
);

--New York

------------------------------------------------------------------------------------------------------------

SELECT name FROM people WHERE phone_number IN
(
    SELECT receiver FROM phone_calls WHERE year = 2023 AND month = 7 AND day = 28 AND duration <= 60 AND caller IN
    (
        SELECT phone_number FROM people WHERE name = 'Bruce'
    )
);

--Accomplice is Robin
