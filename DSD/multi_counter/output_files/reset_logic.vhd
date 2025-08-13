LIBRARY ieee;
USE ieee.std_logic_1164.ALL;

ENTITY reset_logic IS
	PORT (
		--inputs
		clk : IN STD_LOGIC; -- Clock input
		reset_in : IN STD_LOGIC; -- External reset input (active low)
		hrs_bin1 : IN STD_LOGIC_VECTOR(3 DOWNTO 0); -- Binary-coded decimal for units of hours
		hrs_bin10 : IN STD_LOGIC_VECTOR(3 DOWNTO 0); -- Binary-coded decimal for tens of hours

		--outputs
		reset_out : OUT STD_LOGIC

	);
END reset_logic;

ARCHITECTURE reset_logic_impl OF reset_logic IS

	SIGNAL reset_internal : STD_LOGIC := '0';

BEGIN
	PROCESS (clk)
	BEGIN
		IF rising_edge(clk) THEN
			IF reset_in = '0' OR (hrs_bin10 = "0010" AND hrs_bin1 = "0100") THEN
				reset_internal <= '0'; -- External reset or reaching 24
			ELSE
				reset_internal <= '1';
			END IF;
		END IF;
	END PROCESS;

	reset_out <= reset_internal;

END reset_logic_impl;