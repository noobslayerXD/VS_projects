LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;

ENTITY mux1 IS
	PORT (
		-- Input ports
		show : IN STD_LOGIC;
		set_val : IN STD_LOGIC_VECTOR(7 DOWNTO 0);
		try_val : IN STD_LOGIC_VECTOR(7 DOWNTO 0);

		-- Output ports
		mux1_out : OUT STD_LOGIC_VECTOR(7 DOWNTO 0)
	);
END mux1;
ARCHITECTURE mux1_impl OF mux1 IS
BEGIN
	PROCESS (set_val, show)
	BEGIN
		IF show = '0' THEN
			mux1_out <= set_val;
		ELSE
			mux1_out <= try_val;
		END IF;
	END PROCESS;
END mux1_impl;