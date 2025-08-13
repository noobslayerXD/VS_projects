LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;

ENTITY InputLimiter IS
    PORT (
        -- Inputs
        bin_min1 : IN STD_LOGIC_VECTOR(3 DOWNTO 0);
        bin_min10 : IN STD_LOGIC_VECTOR(3 DOWNTO 0);
        bin_hrs1 : IN STD_LOGIC_VECTOR(3 DOWNTO 0);
        bin_hrs10 : IN STD_LOGIC_VECTOR(3 DOWNTO 0);

        -- Outputs
        time_alarm : OUT STD_LOGIC_VECTOR(15 DOWNTO 0)
    );
END InputLimiter;

ARCHITECTURE InputLimiter_impl OF InputLimiter IS
    SIGNAL minutes_count : STD_LOGIC_VECTOR(7 DOWNTO 0) := "00000000";
    SIGNAL hours_count : STD_LOGIC_VECTOR(7 DOWNTO 0) := "00000000";
BEGIN
    PROCESS (bin_min1, bin_min10, bin_hrs1, bin_hrs10)
    BEGIN
        -- Check if minutes and hours are within the valid range (0 to 59 for minutes, 0 to 24 for hours)
        IF bin_min1 <= "1001" AND bin_min10 <= "1001" AND bin_hrs1 <= "1001" AND bin_hrs10 <= "1001" THEN
            -- Output the input values if valid, otherwise output zeros
            minutes_count <= bin_min10 & bin_min1;
            hours_count <= bin_hrs10 & bin_hrs1;

            -- Handle rollover of hours
            IF hours_count = "11000" THEN
                hours_count <= "00000";
            END IF;
        ELSE
            minutes_count <= "00000000";
            hours_count <= "00000000";
        END IF;
        -- Concatenate the limited minutes and hours to form the time_alarm output
        time_alarm <= hours_count & minutes_count;
    END PROCESS;
END InputLimiter_impl;