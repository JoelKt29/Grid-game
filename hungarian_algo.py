# Joel Khayat and Allan Pariente
import numpy as np

class HungarianAlgorithm:
    def my_linear_sum_assignment(self, cost_matrix):
        """
        Solve the linear sum assignment problem.
        Args:
            cost_matrix: cost matrix of bipartite graph.
        Returns:
            array of row and related column indices giving the optimal assignment.
        """
        # check if need to transpose the cost matrix (matrix not squared)
        is_transposed = cost_matrix.shape[1] < cost_matrix.shape[0]

        # handle edge case when cost matrix is empty
        if cost_matrix.shape[0] == 0 or cost_matrix.shape[1] == 0:
            return np.array([]), np.array([])

        if is_transposed:
            cost_matrix = cost_matrix.T  # transpose  matrix

        # convert cost matrix to float
        cost_matrix = cost_matrix.astype(float)

        # initialize dual variables and paths
        row_dual_variables = np.full(cost_matrix.shape[0], 0., dtype=float)
        column_dual_variables = np.full(cost_matrix.shape[1], 0., dtype=float)
        column_path = np.full(cost_matrix.shape[1], -1, dtype=int)
        column_for_row = np.full(cost_matrix.shape[0], -1, dtype=int)
        row_for_column = np.full(cost_matrix.shape[1], -1, dtype=int)

        # iterate over each row to find optimal assignment
        for current_row in range(cost_matrix.shape[0]):
            cost_matrix, row_dual_variables, column_dual_variables, column_path, row_for_column, column_for_row = self.process_assignment_step(
                cost_matrix, row_dual_variables, column_dual_variables, column_path, row_for_column, column_for_row, current_row
            )

        # if transposed, adjust before returning
        if is_transposed:
            sorted_columns = column_for_row.argsort()
            return column_for_row[sorted_columns], sorted_columns
        else:
            return np.arange(cost_matrix.shape[0]), column_for_row

    def update_shortest_path_costs(self, iteration, values):
        remaining_columns, min_value, cost_matrix, current_row, row_dual_variables, column_dual_variables, shortest_path_costs, column_path, lowest_cost, row_for_column, best_index = values

        current_column = remaining_columns[iteration]
        reduced_cost = min_value + cost_matrix[current_row, current_column] - row_dual_variables[current_row] - column_dual_variables[current_column]

        if reduced_cost < shortest_path_costs[current_column]:
            column_path[current_column] = current_row
        shortest_path_costs[current_column] = min(shortest_path_costs[current_column], reduced_cost)

        if (shortest_path_costs[current_column] < lowest_cost) or (shortest_path_costs[current_column] == lowest_cost and row_for_column[current_column] == -1):
            best_index = iteration
        lowest_cost = min(lowest_cost, shortest_path_costs[current_column])

        return remaining_columns, min_value, cost_matrix, current_row, row_dual_variables, column_dual_variables, shortest_path_costs, column_path, lowest_cost, row_for_column, best_index

    def update_remaining_columns(self, values):
        remaining_columns, best_index, row_for_column, sink_column, current_row, visited_columns, num_remaining_columns = values

        current_column = remaining_columns[best_index]
        if row_for_column[current_column] == -1:
            sink_column = current_column
        else:
            current_row = row_for_column[current_column]

        visited_columns[current_column] = True
        num_remaining_columns -= 1
        remaining_columns[best_index] = remaining_columns[num_remaining_columns]

        return remaining_columns, best_index, row_for_column, sink_column, current_row, visited_columns, num_remaining_columns

    def process_shortest_augmenting_path(self, values):
        cost_matrix, row_dual_variables, column_dual_variables, column_path, row_for_column, current_row, min_value, num_remaining_columns, remaining_columns, visited_rows, visited_columns, shortest_path_costs, sink_column = values

        best_index = -1
        lowest_cost = np.inf
        visited_rows[current_row] = True

        for iteration in range(num_remaining_columns):
            remaining_columns, min_value, cost_matrix, current_row, row_dual_variables, column_dual_variables, shortest_path_costs, column_path, lowest_cost, row_for_column, best_index = self.update_shortest_path_costs(
                iteration, (remaining_columns, min_value, cost_matrix, current_row, row_dual_variables, column_dual_variables, shortest_path_costs, column_path, lowest_cost, row_for_column, best_index)
            )

        min_value = lowest_cost
        if min_value == np.inf:
            sink_column = -1

        if sink_column == -1:
            remaining_columns, best_index, row_for_column, sink_column, current_row, visited_columns, num_remaining_columns = self.update_remaining_columns(
                (remaining_columns, best_index, row_for_column, sink_column, current_row, visited_columns, num_remaining_columns)
            )

        return cost_matrix, row_dual_variables, column_dual_variables, column_path, row_for_column, current_row, min_value, num_remaining_columns, remaining_columns, visited_rows, visited_columns, shortest_path_costs, sink_column

    def is_sink_unreachable(self, values):
        sink_column = values[-1]
        return sink_column == -1

    def find_augmenting_path(self, cost_matrix, row_dual_variables, column_dual_variables, column_path, row_for_column, current_row):
        min_value = 0
        num_remaining_columns = cost_matrix.shape[1]
        remaining_columns = np.arange(cost_matrix.shape[1])[::-1]

        visited_rows = np.full(cost_matrix.shape[0], False, dtype=bool)
        visited_columns = np.full(cost_matrix.shape[1], False, dtype=bool)

        shortest_path_costs = np.full(cost_matrix.shape[1], np.inf)
        sink_column = -1

        while self.is_sink_unreachable((cost_matrix, row_dual_variables, column_dual_variables, column_path, row_for_column, current_row, min_value, num_remaining_columns, remaining_columns, visited_rows, visited_columns, shortest_path_costs, sink_column)):
            cost_matrix, row_dual_variables, column_dual_variables, column_path, row_for_column, current_row, min_value, num_remaining_columns, remaining_columns, visited_rows, visited_columns, shortest_path_costs, sink_column = self.process_shortest_augmenting_path(
                (cost_matrix, row_dual_variables, column_dual_variables, column_path, row_for_column, current_row, min_value, num_remaining_columns, remaining_columns, visited_rows, visited_columns, shortest_path_costs, sink_column)
            )

        return sink_column, min_value, visited_rows, visited_columns, shortest_path_costs, column_path

    def update_matching_during_augmentation(self, values):
        column_path, sink_column, row_for_column, column_for_row, current_row, _ = values

        row = column_path[sink_column]
        row_for_column[sink_column] = row

        column_for_row[row], sink_column = sink_column, column_for_row[row]
        break_condition = (row == current_row)

        return column_path, sink_column, row_for_column, column_for_row, current_row, break_condition

    def should_continue_augmentation(self, values):
        break_condition = values[-1]
        return not break_condition

    def process_assignment_step(self, cost_matrix, row_dual_variables, column_dual_variables, column_path, row_for_column, column_for_row, current_row):
        sink_column, min_value, visited_rows, visited_columns, shortest_path_costs, column_path = self.find_augmenting_path(
            cost_matrix, row_dual_variables, column_dual_variables, column_path, row_for_column, current_row
        )

        row_dual_variables[current_row] += min_value
        mask = (visited_rows & (np.arange(cost_matrix.shape[0]) != current_row))
        row_dual_variables += mask * (min_value - shortest_path_costs[column_for_row])

        mask = visited_columns
        column_dual_variables += mask * (shortest_path_costs - min_value)

        break_condition = False
        while self.should_continue_augmentation((column_path, sink_column, row_for_column, column_for_row, current_row, break_condition)):
            column_path, sink_column, row_for_column, column_for_row, current_row, break_condition = self.update_matching_during_augmentation(
                (column_path, sink_column, row_for_column, column_for_row, current_row, break_condition)
            )

        return cost_matrix, row_dual_variables, column_dual_variables, column_path, row_for_column, column_for_row
