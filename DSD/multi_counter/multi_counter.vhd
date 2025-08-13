LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE work.ALL;

ENTITY multi_counter IS
	GENERIC (
		MIN_COUNT : NATURAL := 0; -- min og max count for tæller
		MAX_COUNT : NATURAL := 10
	);
	PORT (
		-- Input ports
		clk : IN STD_LOGIC;
		mode : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
		reset : IN STD_LOGIC;
		clken : IN STD_LOGIC;

		-- Output ports
		count : OUT STD_LOGIC_VECTOR(3 DOWNTO 0);
		cout : OUT STD_LOGIC
	);
END multi_counter;

ARCHITECTURE multi_counter_impl OF multi_counter IS
BEGIN
	counter_proc :
	PROCESS (clk, reset, mode) --process reagerer både clk og reset
		VARIABLE cnt : INTEGER RANGE MIN_COUNT TO MAX_COUNT; -- bruger "variable" for øjeblikkelig opdatering af counter variable
		-- MAX_COUNT betyder IKKE at counteren af sig selv ikke tæller højere end til MAX_COUNT
	BEGIN
		IF reset = '0' THEN-- asynkron reset, ikke afhængig af clk
			-- Reset the counter to 0
			cnt := 0;
			cout <= '0';
		ELSIF (rising_edge(clk)) THEN
			cout <= '0';
			IF clken = '1' THEN
				-- increment counter
				cnt := cnt + 1;
				CASE mode IS
					WHEN "00" =>
						-- Count from 0 to 9 in mode "00"
						IF cnt = 10 THEN
							cnt := 0;
							cout <= '1';
						END IF;
					WHEN "01" =>
						-- Count from 0 to 5 in mode "01"
						IF cnt = 6 THEN
							cnt := 0;
							cout <= '1';
						END IF;
					WHEN OTHERS =>
						-- Count from 0 to 2 in modes "10" and "11"
						IF cnt = 3 THEN
							cnt := 0;
							cout <= '1';
						END IF;
				END CASE;
			END IF;
		END IF;
		-- Output the current count
		count <= STD_LOGIC_VECTOR(to_unsigned(cnt, count'length));
	END PROCESS;
END multi_counter_impl;