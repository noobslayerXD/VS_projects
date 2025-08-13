LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
ENTITY compare IS
	PORT (
		-- Input ports
		set_val : IN STD_LOGIC_VECTOR(7 DOWNTO 0);
		try_val : IN STD_LOGIC_VECTOR(7 DOWNTO 0);
		try : IN STD_LOGIC;
		-- Output ports
		lo : OUT STD_LOGIC;
		hi : OUT STD_LOGIC;
		eq : OUT STD_LOGIC
	);
END compare;
ARCHITECTURE compare_impl OF compare IS
BEGIN
	PROCESS (try_val, try, set_val)
	BEGIN
		IF try = '0' THEN
			-- When set is asserted, the latch stores the input values
			IF try_val > set_val THEN
				hi <= '1';
			END IF;
			IF try_val < set_val THEN
				lo <= '1';
			END IF;
			IF try_val = set_val THEN
				eq <= '1';
			END IF;
		ELSE
			IF try = '1' THEN
				eq <= '0';
				lo <= '0';
				hi <= '0';
			END IF;
		END IF;
	END PROCESS;
END compare_impl;