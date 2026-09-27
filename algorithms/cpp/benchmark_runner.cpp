#include "cp_algorithms.hpp"
#include <chrono>
#include <cstdlib>
#include <iostream>
#include <random>
#include <string>

using Clock = std::chrono::steady_clock;
using cplab::i64;

static volatile i64 sink = 0;

static void run_once(const std::string& slug, const std::vector<i64>& data, const std::string& kind) {
    if (slug == "naive-gcd") { i64 a=std::abs(data[0])+1,b=std::abs(data[1])+1; while(a!=b){if(a>b)a-=b;else b-=a;} sink^=a; }
    else if (slug == "euclidean-gcd") sink ^= cplab::euclidean_gcd(data[0], data[1]);
    else if (slug == "naive-power") { i64 result=1,base=data[0]%1'000'000'007,exponent=std::abs(data[1])%100'000; for(i64 i=0;i<exponent;++i) result=static_cast<i64>((__int128)result*base%1'000'000'007); sink^=result; }
    else if (slug == "binary-exponentiation") sink ^= cplab::binary_exponentiation(data[0], std::abs(data[1]) % 100000, 1'000'000'007);
    else if (slug == "prime-factorization") sink ^= static_cast<i64>(cplab::prime_factorization(std::abs(data[0]) + 1).size());
    else if (slug == "trial-prime") { for(auto raw:data){i64 value=std::abs(raw)+1;bool prime=value>=2;for(i64 d=2;prime&&d<=value/d;++d)if(value%d==0)prime=false;sink^=prime;} }
    else if (slug == "eratosthenes-sieve") sink ^= static_cast<i64>(cplab::eratosthenes_sieve(static_cast<int>(data.size() * 10)).size());
    else if (slug == "euler-linear-sieve") sink ^= static_cast<i64>(cplab::euler_linear_sieve(static_cast<int>(data.size() * 10)).first.size());
    else if (slug == "euler-phi") for (auto value : data) sink ^= cplab::euler_phi(std::abs(value) + 1);
    else if (slug == "binary-search") { auto ordered=data; std::sort(ordered.begin(),ordered.end()); for (std::size_t i = 0; i < std::min<std::size_t>(ordered.size(), 256); ++i) sink ^= cplab::binary_search(ordered, ordered[i]); }
    else if (slug == "merge-sort") sink ^= cplab::merge_sort(data).front();
    else if (slug == "quick-sort") sink ^= cplab::quick_sort(data).front();
    else if (slug == "dsu") { cplab::DisjointSetUnion dsu(static_cast<int>(data.size())); for (int i=1;i<static_cast<int>(data.size());++i) dsu.unite(i-1,i); sink ^= dsu.find(static_cast<int>(data.size()-1)); }
    else if (slug == "dsu-basic") { std::vector<int> parent(data.size());std::iota(parent.begin(),parent.end(),0);auto find=[&parent](int v){while(parent[v]!=v)v=parent[v];return v;};for(int i=1;i<static_cast<int>(data.size());++i)parent[find(i)]=find(i-1);sink^=find(static_cast<int>(data.size()-1)); }
    else if (slug == "naive-prefix") { for(std::size_t end=0;end<data.size();++end) sink^=std::accumulate(data.begin(),data.begin()+end+1,i64{0}); }
    else if (slug == "fenwick-tree") { cplab::FenwickTree tree(data); for (int i=0;i<static_cast<int>(data.size());++i) sink ^= tree.prefix_sum(i); }
    else if (slug == "segment-tree") { cplab::SegmentTree tree(data); for (int i=1;i<=static_cast<int>(data.size());++i) sink ^= tree.range_sum(0,i); }
    else if (slug == "bfs" || slug == "dfs" || slug == "dijkstra") {
        int n = static_cast<int>(data.size());
        std::vector<std::pair<int,int>> pairs;
        if (kind == "dense-graph") {
            for(int left=0;left<n;++left) for(int right=left+1;right<n;++right)
                if ((std::abs(data[left])*31 + std::abs(data[right])*17 + left*13 + right) % 10000 < 1500) pairs.push_back({left,right});
        } else if (kind == "random-tree") {
            for(int i=1;i<n;++i) pairs.push_back({static_cast<int>(std::abs(data[i]) % i),i});
        } else {
            for(int i=1;i<n;++i) pairs.push_back({i-1,i});
            if (kind == "sparse-graph") for(int i=0;i+2<n;i+=7) pairs.push_back({i,i+2});
        }
        if (slug == "dijkstra") { std::vector<std::vector<std::pair<int,i64>>> graph(n); for(auto [left,right]:pairs){ i64 weight=std::abs(data[right])%100+1; graph[left].push_back({right,weight}); graph[right].push_back({left,weight}); } auto result=cplab::dijkstra(graph,0); sink ^= result.back()==std::numeric_limits<i64>::max()?0:result.back(); }
        else { std::vector<std::vector<int>> graph(n); for(auto [left,right]:pairs){ graph[left].push_back(right); graph[right].push_back(left); } sink ^= slug=="bfs" ? cplab::bfs(graph,0).first.back() : cplab::dfs(graph,0).back(); }
    } else throw std::invalid_argument("unsupported benchmark algorithm");
}

int main(int argc, char** argv) {
    if (argc != 6) return 2;
    const std::string slug = argv[1], kind = argv[5];
    const int size = std::stoi(argv[2]), seed = std::stoi(argv[3]), runs = std::stoi(argv[4]);
    if (size < 1 || runs < 1) return 3;
    std::mt19937 generator(seed); std::uniform_int_distribution<i64> distribution(1, 1'000'000);
    std::vector<i64> data(size); for (auto& value : data) value = distribution(generator);
    if (kind == "sorted") std::sort(data.begin(), data.end());
    else if (kind == "reverse-sorted") std::sort(data.rbegin(), data.rend());
    else if (kind == "duplicate-heavy") for (auto& value : data) value %= 16;
    std::cout << "[";
    for (int run = 0; run < runs; ++run) {
        const auto started = Clock::now(); run_once(slug, data, kind); const auto ended = Clock::now();
        const double milliseconds = std::chrono::duration<double, std::milli>(ended - started).count();
        if (run) std::cout << ','; std::cout << milliseconds;
    }
    std::cout << "]\n";
}
