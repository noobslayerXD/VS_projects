library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity multi_counter is
    Port ( clk : in STD_LOGIC;
           reset : in STD_LOGIC;
           mode : in STD_LOGIC_VECTOR(1 downto 0);
           count : out STD_LOGIC_VECTOR(1 downto 0);
           cout : out STD_LOGIC;
           seg : out STD_LOGIC_VECTOR(6 downto 0));
end multi_counter;

architecture Behavioral of multi_counter is
    signal counter : STD_LOGIC_VECTOR(1 downto 0) := "00";

begin
    process (clk, reset, mode)
    begin
        if reset = '1' then
            counter <= "00"; -- Reset the counter to 0
        elsif rising_edge(clk) then
            case mode is
                when "00" =>
                    -- Count from 0 to 9 in mode "00"
                    if counter = "1001" then
                        counter <= "00";
                    else
                        counter <= std_logic_vector(unsigned(counter) + 1);
                    end if;
                when "01" =>
                    -- Count from 0 to 5 in mode "01"
                    if counter = "0101" then
                        counter <= "00";
                    else
                        counter <= std_logic_vector(unsigned(counter) + 1);
                    end if;
                when others =>
                    -- Count from 0 to 2 in modes "10" and "11"
                    if counter = "0010" then
                        counter <= "00";
                    else
                        counter <= std_logic_vector(unsigned(counter) + 1);
                    end if;
            end case;
        end if;
    end process;

    count <= counter; -- Output the binary counter value
    cout <= '1' when counter = "11" else '0'; -- Carry-out when counter resets to 0

    -- 7-segment decoder mapping
    process (counter)
    begin
        case counter is
            when "00" => seg <= "1000000"; -- Display '0'
            when "01" => seg <= "1111001"; -- Display '1'
            when "10" => seg <= "0100100"; -- Display '2'
            when "11" => seg <= "0110000"; -- Display '3'
            when others => seg <= "1111111"; -- Display blank (error case)
        end case;
    end process;

end Behavioral;
