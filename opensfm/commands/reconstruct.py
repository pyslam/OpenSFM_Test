import logging
import time

from opensfm import dataset
from opensfm import io
from opensfm import reconstruction

logger = logging.getLogger(__name__)


class Command:
    name = 'reconstruct'
    help = "Compute the reconstruction"

    def add_arguments(self, parser):
        parser.add_argument('dataset', help='dataset to process')

    def run(self, args):
        start = time.time()
        data = dataset.DataSet(args.dataset)
        report = reconstruction.incremental_reconstruction(data)
        end = time.time()
        with open(data.profile_log(), 'a') as fout:
            fout.write('reconstruct: {0}, error: {1}, bundle time: {2}\n'.format(end - start, \
                reconstruction.get_avg_reprojection_error(), \
                reconstruction.get_total_bundle_time()))
        data.save_report(io.json_dumps(report), 'reconstruction.json')
