import collections
import itertools

from time import time

import ROOT

ChainCluster = collections.namedtuple(
    "ChainCluster", ["start", "end", "offset", "filetuple", "treenentries", "treename"])
FileAndIndex = collections.namedtuple("FileAndIndex", ["filename", "fileindex"])
TreeRange = collections.namedtuple("TreeRange", ["rangeid", "globalstart", "globalend",
                                   "localstarts", "localends", "filelist", "treesnentries", "treenames", "friendinfo"])


def get_clusters(treenames, filenames):

    clusters = []

    offset = 0
    fileindex = 0

    for treename, filename in zip(treenames, filenames):
        f = ROOT.TFile.Open(filename)
        t = f.Get(treename)

        entries = t.GetEntriesFast()
        it = t.GetClusterIterator(0)
        start = it()
        end = 0

        while start < entries:
            end = it()
            clusters.append(ChainCluster(start, end, offset, FileAndIndex(filename, fileindex), entries, treename))
            start = end

        fileindex += 1
        offset += entries

    return clusters


def _n_even_chunks(iterable, n_chunks):

    last = 0
    itlenght = len(iterable)
    for i in range(1, n_chunks + 1):
        cur = int(round(i * (itlenght / n_chunks)))
        yield iterable[last:cur]
        last = cur


def get_clustered_ranges(clustersinfiles, npartitions, friendinfo=None):

    clustersbypartition = _n_even_chunks(clustersinfiles, npartitions)

    clustered_ranges = []
    rangeid = 0
    for partition in clustersbypartition:

        localstarts = []
        localends = []
        filelist = []
        treesnentries = []
        treenames = []

        for _, clustersinsamefileiter in itertools.groupby(partition, lambda cluster: cluster.filetuple.fileindex):

            clustersinsamefilelist = list(clustersinsamefileiter)

            localstarts.append(min(clustersinsamefilelist).start)
            localends.append(max(clustersinsamefilelist).end)
            filelist.append(clustersinsamefilelist[0].filetuple.filename)
            treesnentries.append(clustersinsamefilelist[0].treenentries)
            treenames.append(clustersinsamefilelist[0].treename)

        firstclusterinpartition = partition[0]
        partitionoffset = firstclusterinpartition.offset

        lastclusterinpartition = partition[-1]

        globalstart = firstclusterinpartition.start
        globalend = lastclusterinpartition.end + lastclusterinpartition.offset - partitionoffset

        clustered_ranges.append(TreeRange(rangeid, globalstart, globalend, localstarts,
                                localends, filelist, treesnentries, treenames, friendinfo))
        rangeid += 1

    return clustered_ranges


treenames = ["Events"] * 100
filenames = [("root://eospublic.cern.ch/"
              "/eos/root-eos/benchmark/CMSOpenDataDimuon/"
              "Run2012BC_DoubleMuParked_Muons_{}.root").format(i)
             for i in range(1, 101)
             ]
npartitions = 10000

if __name__ == "__main__":

    with open("benchmarks/get_clusters.csv", "a+") as f:
        for _ in range(5):
            print("Retrieving clusters from file...")
            start_clusters = time()
            clustersinfiles = get_clusters(treenames, filenames)
            end_clusters = time()

            print("Bulding ranges...")
            start_ranges = time()
            clusteredranges = get_clustered_ranges(clustersinfiles, npartitions)
            end_ranges = time()
            f.write("{},{}\n".format(round(end_clusters - start_clusters, 2), round(end_ranges - start_ranges, 2)))
