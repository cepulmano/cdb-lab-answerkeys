-- You are trying to find out if there is a correlation between the time it takes for a plane to land and the time it takes for a plane to depart.
--You are tasked with finding all flights where the arrival delay is longer than the departure delay. Show the entire name of the airline (25pts)

SELECT p.mkt_carrier_fl_num, cc.carrier_desc, p.arr_delay_new, p.dep_delay_new
FROM performance p
JOIN codes_carrier cc on p.mkt_carrier = cc.carrier_code
WHERE p.arr_delay_new > p.dep_delay_new;

-- United Airlines is launching an investigation to audit the quality of their service.
-- They are looking specifically at flights arriving in Chicago (ORD) or San Francisco (SFO).
-- They want to know the flights where the departure delay exceeds the monthly average of flight route. (25pts)

WITH flight_ave AS (
    SELECT EXTRACT("YEAR" FROM fl_date) "the_year", EXTRACT("MONTH" FROM fl_date) "the_month", origin, dest, AVG(dep_delay_new) "monthly_average"
    FROM performance
    WHERE dest IN ('ORD','SFO') AND mkt_carrier = 'UA'
    GROUP BY the_month, the_year, origin, dest
)
SELECT p.mkt_carrier_fl_num, p.mkt_carrier, p.origin, p.dest, p.dep_delay_new, fa.monthly_average
FROM performance p
JOIN flight_ave fa
    ON EXTRACT("YEAR" FROM p.fl_date) = fa.the_year
    AND EXTRACT("MONTH" FROM p.fl_date) = fa.the_month
    AND p.origin = fa.origin
    AND p.dest = fa.dest
WHERE
    p.dep_delay_new > fa.monthly_average;

-- Several airlines are part of an air alliance, which allows transfers between carriers to be made more easily. This is a list of carrier codes and their air alliances:

CREATE OR replace function getAlliances(in x CHAR(2), out alliance VARCHAR(60)) AS $$
begin
    CASE
        WHEN x = 'AA' THEN alliance := 'One World';
        WHEN x = 'DL' THEN alliance := 'SkyTeam';
        WHEN x IN ('HA','UA') THEN alliance := 'Star Alliance';
        ELSE alliance := 'No Alliance';
    END CASE;
END;
$$ language plpgsql;

SELECT DISTINCT(carrier_code), getAlliances(carrier_code) FROM codes_carrier ORDER BY carrier_code;