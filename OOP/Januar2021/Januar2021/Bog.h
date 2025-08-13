#pragma once
#include <string>

class Bog 
{
private:
	std::string titel_;
	std::string forfatter_;
public:
	
	Bog(const std::string& titel, const std::string& forfatter);
	
	virtual ~Bog();
	virtual int getMinimumsAlder() const =0;

	void print() const;

	void setTitel(const std::string& titel) ;
	void setForfatter(const std::string& forfatter) ;
	std::string getTitel() const;
	std::string getForfatter() const;


};
