#include <bits/stdc++.h>
using namespace std;
 
#define M 1000000007
 
#define mp make_pair
#define pb push_back
#define tri pair<int, pair<int, int> >
#define TRI(a,b,c) (make_pair(a,make_pair(b,c)))
 
typedef long long ll;
typedef long double ld;

ll pref[100001], l[100000], r[100000], v[100000];

vector<pair<ll, ll> > adj[100001];

void dfs(int i)
{
	for(auto j: adj[i])
	{
		if(pref[j.first] == -1)
		{
			pref[j.first] = pref[i] ^ j.second;
			dfs(j.first);
		}
	}
}

int main() 
{
    memset(pref, -1, sizeof(pref));
    pref[0] = 0;
    for(int i=0; i<100000; i++)
    {
    	cin>>l[i]>>r[i]>>v[i];
    	adj[l[i]-1].pb(mp(r[i], v[i]));
    	adj[r[i]].pb(mp(l[i]-1, v[i]));
    }
    dfs(0);
    for(int i=1; i<=100000; i++)
    {
    	if(pref[i] == -1)
    	{
    		pref[i] = 0;
    		dfs(i);
    	}
    }
    /* for(int i=0; i<100000; i++)
    {
    	if((pref[l[i]-1] ^ pref[r[i]]) != v[i])
    	{
    		cout<<"Error in constraint "<<i+1<<" "<<l[i]<<" "<<r[i]<<" "<<v[i]<<" "<<pref[l[i]-1]<<" "<<pref[r[i]]<<" "<<(pref[l[i]-1] ^ pref[r[i]])<<endl;
    		return 0;
    	}
    }
    cout<<"All correct!\n";*/
    for(int i=1; i<= 100000; i++)
    {
    	cout<<(pref[i] ^ pref[i-1])<<'\n';
    }
    return 0;
}