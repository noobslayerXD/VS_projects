using System;

namespace RPG
{
	public class Battle
	{
		public void BattleIntro()
		{
			Console.WriteLine("The flower garden is on fire, and a war is raging");
			Fighting();
		}
		public void Fighting()
        {
			Console.WriteLine("What do you do?");
        }
	}
}